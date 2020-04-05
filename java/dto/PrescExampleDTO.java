package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("presc_example")
public class PrescExampleDTO {
    @Primary
    @AutoInc
    public int prescExampleId;
    @MysqlColName("m_iyakuhincode")
    public int iyakuhincode;
    @MysqlColName("m_master_valid_from")
    @TypeHint({"date"})
    public String masterValidFrom;
    @MysqlColName("m_amount")
    public String amount;
    @MysqlColName("m_usage")
    public String usage;
    @MysqlColName("m_days")
    public int days;
    @MysqlColName("m_category")
    public int category;
    @MysqlColName("m_comment")
    public String comment;

    public PrescExampleDTO copy(){
        PrescExampleDTO dst = new PrescExampleDTO();
        dst.prescExampleId = prescExampleId;
        dst.iyakuhincode = iyakuhincode;
        dst.masterValidFrom = masterValidFrom;
        dst.amount = amount;
        dst.usage = usage;
        dst.days = days;
        dst.category = category;
        dst.comment = comment;
        return dst;
    }
}
