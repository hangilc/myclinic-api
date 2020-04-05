package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("hotline")
public class HotlineDTO {
    @Primary
    @AutoInc
    public int hotlineId;
    public String message;
    public String sender;
    public String recipient;
    @MysqlColName("m_datetime")
    @TypeHint({"datetime"})
    public String postedAt;
}
