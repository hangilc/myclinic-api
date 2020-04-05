package dev.myclinic.dto;

import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("shouki")
public class ShoukiDTO {
    @Primary
    public int visitId;
    public String shouki;

    public static ShoukiDTO copy(ShoukiDTO src){
        ShoukiDTO dst = new ShoukiDTO();
        dst.visitId = src.visitId;
        dst.shouki = src.shouki;
        return dst;
    }

    @Override
    public String toString() {
        return "ShoukiDTO{" +
                "visitId=" + visitId +
                ", shouki='" + shouki + '\'' +
                '}';
    }
}
