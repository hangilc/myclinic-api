package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

import java.util.Objects;

@MysqlTable("visit_text")
public class TextDTO {
    @Primary
    @AutoInc
    public int textId;
    public int visitId;
    public String content;

    public static TextDTO create(int visitId, String content){
        TextDTO text = new TextDTO();
        text.visitId = visitId;
        text.content = content;
        return text;
    }

    public TextDTO copy(){
        TextDTO textDTO = new TextDTO();
        textDTO.textId = textId;
        textDTO.visitId = visitId;
        textDTO.content = content;
        return textDTO;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        TextDTO textDTO = (TextDTO) o;
        return textId == textDTO.textId &&
                visitId == textDTO.visitId &&
                Objects.equals(content, textDTO.content);
    }

    @Override
    public int hashCode() {
        return Objects.hash(textId, visitId, content);
    }

    @Override
    public String toString() {
        return "TextDTO{" +
                "textId=" + textId +
                ", visitId=" + visitId +
                ", content='" + content + '\'' +
                '}';
    }
}
