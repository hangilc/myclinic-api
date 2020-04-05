package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

import java.util.Objects;

public class UpdateHokenDTO {
    public int visitId;
    @nullable
    public int shahokokuhoId;
    @nullable
    public int koukikoureiId;
    @nullable
    public int roujinId;
    @nullable
    public int kouhi1Id;
    @nullable
    public int kouhi2Id;
    @nullable
    public int kouhi3Id;
}

