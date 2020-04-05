package dev.myclinic.dto;

import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("pharma_queue")
public class PharmaQueueDTO {
    @Primary
    public int visitId;
    public int pharmaState;

    public static PharmaQueueDTO copy(PharmaQueueDTO src){
        PharmaQueueDTO dst = new PharmaQueueDTO();
        dst.visitId = src.visitId;
        dst.pharmaState = src.pharmaState;
        return dst;
    }

    @Override
    public String toString() {
        return "PharmaQueueDTO{" +
                "visitId=" + visitId +
                ", pharmaState=" + pharmaState +
                '}';
    }
}
