package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.DiseaseAdjDTO;

public class DiseaseAdjUpdated implements PracticeLogBody {

    public DiseaseAdjDTO prev;
    public DiseaseAdjDTO updated;

    public DiseaseAdjUpdated() {
    }

    public DiseaseAdjUpdated(DiseaseAdjDTO prev, DiseaseAdjDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}