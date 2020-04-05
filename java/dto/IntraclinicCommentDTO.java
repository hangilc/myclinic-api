package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("intraclinic_comment")
public class IntraclinicCommentDTO {
    @Primary
    @AutoInc
    public int id;
    public String name;
    public String content;
    public int postId;
    @TypeHint({"date"})
    public String createdAt;

    @Override
    public String toString() {
        return "IntraclinicCommentDTO{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", content='" + content + '\'' +
                ", postId=" + postId +
                ", createdAt='" + createdAt + '\'' +
                '}';
    }
}
