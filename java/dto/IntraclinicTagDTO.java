package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("intraclinic_tag")
public class IntraclinicTagDTO {

    @Primary
    @AutoInc
    @MysqlColName("id")
    public int tagId;
    public String name;

    @Override
    public String toString() {
        return "IntraclinicTagDTO{" +
                "tagId=" + tagId +
                ", name='" + name + '\'' +
                '}';
    }
}
