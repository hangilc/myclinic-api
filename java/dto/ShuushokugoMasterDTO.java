package dev.myclinic.dto;

import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("shuushokugo_master")
public class ShuushokugoMasterDTO {
    @Primary
    public int shuushokugocode;
    public String name;

    @Override
    public String toString() {
        return "ShuushokugoMasterDTO{" +
                "shuushokugocode=" + shuushokugocode +
                ", name='" + name + '\'' +
                '}';
    }
}
