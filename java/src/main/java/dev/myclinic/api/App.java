package dev.myclinic.api;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.FieldDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.expr.AnnotationExpr;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.type.PrimitiveType;
import com.github.javaparser.ast.type.Type;

import java.io.File;
import java.util.*;
import java.util.stream.Collectors;

public class App {
    public static void main(String[] args) throws Exception {
        if (args.length > 0) {
            String cmd = args[0];
            switch (cmd) {
                case "dto": {
                    new App().startDto();
                    break;
                }
                case "practice-log": {
                    new App().startPracticeLog();
                    break;
                }
                case "service": {
                    new App().startService();
                    break;
                }
                default:
                    usage();
                    System.exit(1);
            }
        } else {
            usage();
            System.exit(1);
        }
    }

    private static void usage() {
        System.err.println("Usage: App {dto|practice-log|service}");
    }

    @SuppressWarnings("OptionalGetWithoutIsPresent")
    private void startService() throws Exception {
        Map<String, Object> result = new HashMap<>();
        Map<String, Object> messages = new HashMap<>();
        result.put("protocol", "MyclinicService");
        result.put("messages", messages);
        File path = new File("./Service.java");
        CompilationUnit unit = new JavaParser().parse(path.toPath()).getResult().orElse(null);
        if (unit == null) {
            throw new RuntimeException("Cannot parse: " + path.toString());
        }
        ClassOrInterfaceDeclaration outer = unit.getClassByName("Service").orElse(null);
        if (outer == null) {
            throw new RuntimeException("Cannot find Service class.");
        }
        for (var member : outer.getMembers()) {
            if (member.isClassOrInterfaceDeclaration()) {
                ClassOrInterfaceDeclaration decl = member.asClassOrInterfaceDeclaration();
                if (decl.isInterface() && decl.getNameAsString().equals("ServerAPI")) {
                    for (MethodDeclaration meth : decl.getMethods()) {
                        Type methType = meth.getType();
                        if (methType.isClassOrInterfaceType()) {
                            ClassOrInterfaceType methClass = methType.asClassOrInterfaceType();
                            String wrapperClass = methClass.getNameAsString();
                            if (wrapperClass.equals("CompletableFuture")) {
                                NodeList<Type> argTypes = methClass.getTypeArguments().orElse(null);
                                if (argTypes.size() != 1) {
                                    throw new RuntimeException("Unexpected return type: " + member.toString());
                                }
                                Map<String, Object> msg = new HashMap<>();
                                messages.put(meth.getNameAsString(), msg);
                                msg.put("doc", "");
                                Type retType = argTypes.get(0);
                                msg.put("response", getAvroType(retType));
                                List<Map<String, Object>> params = new ArrayList<>();
                                msg.put("request", params);
                                for (Parameter param : meth.getParameters()) {
                                    Map<String, Object> para = getAvroTypeAsMap(param.getType());
                                    if( param.isAnnotationPresent("nullable") ){
                                        Object t = para.get("type");
                                        para.put("type", List.of("null", t));
                                    }
                                    if (param.isAnnotationPresent("Query")) {
                                        String q = getSingleValueAnnotationValue(
                                                param.getAnnotationByName("Query").get());
                                        para.put("name", q);
                                    } else if (param.isAnnotationPresent("Body")) {
                                        para.put("name", param.getNameAsString().replaceFirst("DTO$", ""));
                                        para.put("isBody", true);
                                    } else {
                                        throw new RuntimeException("Unannotated request param: " +
                                                meth.toString());
                                    }
                                    params.add(para);
                                }
                                if (meth.isAnnotationPresent("NoDatabase") ){
                                    msg.put("noDatabase", true);
                                }
                                if (meth.isAnnotationPresent("Streaming") ){
                                    msg.put("isStreaming", true);
                                }
                                if (meth.isAnnotationPresent("GET")) {
                                    String url = getSingleValueAnnotationValue(
                                            meth.getAnnotationByName("GET").get());
                                    msg.put("url", url);
                                    msg.put("httpMethod", "get");
                                } else if (meth.isAnnotationPresent("POST")) {
                                    String url = getSingleValueAnnotationValue(
                                            meth.getAnnotationByName("POST").get());
                                    msg.put("url", url);
                                    msg.put("httpMethod", "post");
                                } else {
                                    throw new RuntimeException("Cannot find http method: " + decl);
                                }
                            }
                        }
                    }
                }
            }
        }
        outputResult(result);
    }

    private String getSingleValueAnnotationValue(AnnotationExpr annot) {
        return annot
                .asSingleMemberAnnotationExpr()
                .getMemberValue()
                .asStringLiteralExpr()
                .getValue();
    }

    private List<String> getAnnotationValues(AnnotationExpr annot) {
        return annot
                .asSingleMemberAnnotationExpr()
                .getMemberValue()
                .asArrayInitializerExpr()
                .getValues()
                .stream()
                .map(n -> n.asLiteralStringValueExpr().getValue())
                .collect(Collectors.toList());
    }

    private void startPracticeLog() throws Exception {
        List<Map<String, Object>> resultList = new ArrayList<>();
        for (File file : Objects.requireNonNull(new File("./practicelog").listFiles())) {
            if (!(file.isFile() && file.getPath().endsWith(".java"))) {
                continue;
            }
            CompilationUnit unit = new JavaParser().parse(file.toPath()).getResult().orElse(null);
            if (unit == null) {
                throw new RuntimeException("Cannot parse source: " + file.getName());
            }
            String origName = file.getName().replaceAll("\\.java$", "");
            if (unit.getInterfaceByName(origName).isPresent()) {
                continue;
            }
            ClassOrInterfaceDeclaration decl = unit.getClassByName(origName).orElse(null);
            if (decl == null) {
                throw new RuntimeException("Cannot find class: " + file.getName());
            }
            Map<String, Object> item = new HashMap<>();
            item.put("type", "record");
            item.put("name", origName);
            List<Map<String, Object>> fields = new ArrayList<>();
            for (FieldDeclaration field : decl.getFields()) {
                for (var variable : field.getVariables()) {
                    Map<String, Object> f = new HashMap<>();
                    f.put("name", variable.getNameAsString());
                    f.put("type", getAvroType(variable.getType()));
                    fields.add(f);
                }
            }
            item.put("fields", fields);
            resultList.add(item);
        }
        outputResult(resultList);
    }

    private void outputResult(Object obj) throws JsonProcessingException {
        ObjectMapper mapper = new ObjectMapper();
        String output = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(obj);
        System.out.println(output);
    }

    @SuppressWarnings("OptionalGetWithoutIsPresent")
    private void startDto() throws Exception {
        List<Map<String, Object>> resultList = new ArrayList<>();
        for (File file : Objects.requireNonNull(new File("./dto").listFiles())) {
            if (!(file.isFile() && file.getPath().endsWith(".java"))) {
                continue;
            }
            CompilationUnit unit = new JavaParser().parse(file.toPath()).getResult().orElse(null);
            if (unit == null) {
                throw new RuntimeException("Cannot parse source: " + file.getName());
            }
            String origName = file.getName().replaceAll("\\.java$", "");
            ClassOrInterfaceDeclaration decl = unit.getClassByName(origName).orElse(null);
            if (decl == null) {
                throw new RuntimeException("Cannot find class: " + file.getName());
            }
            Map<String, Object> item = new HashMap<>();
            if (decl.isAnnotationPresent("MysqlTable")) {
                AnnotationExpr expr = decl.getAnnotationByName("MysqlTable").orElse(null);
                if (expr == null) {
                    throw new RuntimeException("Invalid MysqlTable annotation: " + decl.toString());
                }
                String table = expr.asSingleMemberAnnotationExpr().getMemberValue()
                        .asStringLiteralExpr().getValue();
                item.put("mysqlTable", table);
            }
            String name = origName.replaceFirst("DTO$", "");
            item.put("type", "record");
            item.put("name", name);
            List<Map<String, Object>> fields = new ArrayList<>();
            for (FieldDeclaration field : decl.getFields()) {
                boolean isPrimary = field.isAnnotationPresent("Primary");
                boolean isAutoInc = field.isAnnotationPresent("AutoInc");
                boolean hasMysqlColName = field.isAnnotationPresent("MysqlColName");
                boolean hasTypeHint = field.isAnnotationPresent("TypeHint");
                boolean isNullable = field.isAnnotationPresent("nullable");
                for (var variable : field.getVariables()) {
                    Map<String, Object> f = getAvroTypeAsMap(variable.getType());
                    String fname = variable.getNameAsString();
                    if( fname.endsWith("DTO") ){
                        f.put("name", fname.replaceAll("DTO$", ""));
                        f.put("jsonName", fname);
                    } else {
                        f.put("name", fname);
                    }
                    fields.add(f);
                    if (isPrimary) {
                        f.put("isPrimaryKey", true);
                    }
                    if (isAutoInc) {
                        f.put("isAutoInc", true);
                    }
                    if (hasMysqlColName) {
                        f.put("mysqlColName", getSingleValueAnnotationValue(
                                field.getAnnotationByName("MysqlColName").get()));
                    }
                    if (hasTypeHint) {
                        f.put("typeHints", getAnnotationValues(
                                field.getAnnotationByName("TypeHint").get()));
                    }
                    if (isNullable) {
                        Object t = f.get("type");
                        f.put("type", List.of("null", t));
                    }
                }
            }
            item.put("fields", fields);
            resultList.add(item);
        }
        outputResult(resultList);
    }

    private Map<String, Object> getAvroTypeAsMap(Type type) {
        Map<String, Object> item = new HashMap<String, Object>();
        if (type.isPrimitiveType()) {
            PrimitiveType primitiveType = type.asPrimitiveType();
            String name = primitiveType.asString();
            if ("char".equals(name)) {
                item.put("type", "string");
                return item;
            } else {
                item.put("type", name);
                return item;
            }
        } else if (type.isClassOrInterfaceType()) {
            ClassOrInterfaceType cls = type.asClassOrInterfaceType();
            String name = cls.getNameAsString();
            if (name.equals("List")) {
                NodeList<Type> args = cls.getTypeArguments().orElse(null);
                if (args == null || args.size() != 1) {
                    throw new RuntimeException("Cannot handle List type: " + type.toString());
                }
                Type argType = args.get(0);
                item.put("type", "array");
                item.put("items", getAvroType(argType));
                return item;
            } else if(name.equals("Map")){
                NodeList<Type> args = cls.getTypeArguments().orElse(null);
                if (args == null || args.size() != 2) {
                    throw new RuntimeException("Cannot handle Map type: " + type.toString());
                }
                Type keyType = args.get(0);
                Type valType = args.get(1);
                item.put("type", "map");
                item.put("values", getAvroType(valType));
                item.put("keys", getAvroType(keyType));
                return item;
            } else if (name.equals("String")) {
                item.put("type", "string");
                return item;
            } else if (name.equals("LocalDate")) {
                item.put("type", "string");
                item.put("typeHints", List.of("date"));
                return item;
            } else if (name.equals("LocalDateTime")) {
                item.put("type", "string");
                item.put("typeHints", List.of("datetime"));
                return item;
            } else if (cls.isBoxedType()) {
                switch (name) {
                    case "Integer":
                        item.put("type", "int");
                        return item;
                    case "Double":
                        item.put("type", "double");
                        return item;
                    case "Character":
                        item.put("type", "string");
                        return item;
                    case "Boolean":
                        item.put("type", "boolean");
                        return item;
                    default:
                        throw new RuntimeException("Cannot hanlde boxed type: " + name);
                }
            } else {
                item.put("type", name.replaceFirst("DTO$", ""));
                return item;
            }
        } else {
            item.put("type", type.toString());
            return item;
        }
    }

    private Object getAvroType(Type type) {
        var asMap = getAvroTypeAsMap(type);
        if( asMap.keySet().size() == 1 ){
            return asMap.get("type");
        } else {
            return asMap;
        }
//        if (type.isPrimitiveType()) {
//            PrimitiveType primitiveType = type.asPrimitiveType();
//            String name = primitiveType.asString();
//            switch (name) {
//                case "char":
//                    return "string";
//                default:
//                    return name;
//            }
//        } else if (type.isClassOrInterfaceType()) {
//            ClassOrInterfaceType cls = type.asClassOrInterfaceType();
//            String name = cls.getNameAsString();
//            if (name.equals("List")) {
//                NodeList<Type> args = cls.getTypeArguments().orElse(null);
//                if (args.size() != 1) {
//                    throw new RuntimeException("Cannot hanlde List type: " + type.toString());
//                }
//                Type argType = args.get(0);
//                Map<String, Object> item = new HashMap<>();
//                item.put("type", "array");
//                item.put("items", getAvroType(argType));
//                return item;
//            } else if (name.equals("String")) {
//                return "string";
//            } else if (name.equals("LocalDate")) {
//                Map<String, Object> item = new HashMap<>();
//                item.put("type", "string");
//                item.put("typeHints", List.of("date"));
//                return item;
//            } else if (name.equals("LocalDateTime")) {
//                Map<String, Object> item = new HashMap<>();
//                item.put("type", "string");
//                item.put("typeHints", List.of("datetime"));
//                return item;
//            } else if (cls.isBoxedType()) {
//                switch (name) {
//                    case "Integer":
//                        return "int";
//                    case "Double":
//                        return "double";
//                    case "Character":
//                        return "string";
//                    case "Boolean":
//                        return "boolean";
//                    default:
//                        throw new RuntimeException("Cannot hanlde boxed type: " + name);
//                }
//            } else {
//                return name.replaceFirst("DTO$", "");
//            }
//        } else {
//            return type.toString();
//        }
    }
}
