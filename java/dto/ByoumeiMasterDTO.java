package dev.myclinic.dto;

import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("shoubyoumei_master_arch")
public class ByoumeiMasterDTO {

    @Primary
    public int shoubyoumeicode;
    public String name;
    @Primary
    public String validFrom;
    public String validUpto;

    @Override
    public String toString() {
        return "ByoumeiMasterDTO{" +
                "shoubyoumeicode=" + shoubyoumeicode +
                ", name='" + name + '\'' +
                ", validFrom='" + validFrom + '\'' +
                ", validUpto='" + validUpto + '\'' +
                '}';
    }
}
