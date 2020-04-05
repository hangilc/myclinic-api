package dev.myclinic.dto;

import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("pharma_drug")
public class PharmaDrugDTO {
    @Primary
    public int iyakuhincode;
    public String description;
    public String sideeffect;

    @Override
    public String toString() {
        return "PharmaDrugDTO{" +
                "iyakuhincode=" + iyakuhincode +
                ", description='" + description + '\'' +
                ", sideeffect='" + sideeffect + '\'' +
                '}';
    }
}
