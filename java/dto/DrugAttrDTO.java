package dev.myclinic.dto;

import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

import java.util.Objects;

@MysqlTable("drug_attr")
public class DrugAttrDTO {
    @Primary
    public int drugId;
    public String tekiyou;

    public static DrugAttrDTO copy(DrugAttrDTO src) {
        DrugAttrDTO dst = new DrugAttrDTO();
        dst.drugId = src.drugId;
        dst.tekiyou = src.tekiyou;
        return dst;
    }

    public static boolean isEmpty(DrugAttrDTO attr) {
        return attr.tekiyou == null || attr.tekiyou.isEmpty();
    }

    public static String getTekiyou(DrugAttrDTO attr, String tekiyou){
        return attr == null ? null : attr.tekiyou;
    }

    public static DrugAttrDTO setTekiyou(int drugId, DrugAttrDTO attr, String tekiyou){
        if( attr == null ){
            attr = new DrugAttrDTO();
            attr.drugId = drugId;
        }
        attr.tekiyou = tekiyou;
        if( isEmpty(attr) ){
            attr = null;
        }
        return attr;
    }

    public static DrugAttrDTO deleteTekiyou(int drugId, DrugAttrDTO attr){
        return setTekiyou(drugId, attr, null);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        DrugAttrDTO that = (DrugAttrDTO) o;
        return drugId == that.drugId &&
                Objects.equals(tekiyou, that.tekiyou);
    }

    @Override
    public int hashCode() {
        return Objects.hash(drugId, tekiyou);
    }

    @Override
    public String toString() {
        return "DrugAttrDTO{" +
                "drugId=" + drugId +
                ", tekiyou='" + tekiyou + '\'' +
                '}';
    }
}
