package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("intraclinic_post")
public class IntraclinicPostDTO {
    @Primary
    @AutoInc
    public Integer id;
    public String content;
    @TypeHint({"date"})
    public String createdAt;

    @Override
    public String toString() {
        return "IntraclinicPostDTO{" +
                "id=" + id +
                ", content='" + content + '\'' +
                ", createdAt='" + createdAt + '\'' +
                '}';
    }
}
