package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.DiseaseDTO;

public class DiseaseUpdated implements PracticeLogBody {

    public DiseaseDTO prev;
    public DiseaseDTO updated;

    public DiseaseUpdated() {
    }

    public DiseaseUpdated(DiseaseDTO prev, DiseaseDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}