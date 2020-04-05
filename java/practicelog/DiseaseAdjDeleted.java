package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.DiseaseAdjDTO;

public class DiseaseAdjDeleted implements PracticeLogBody {

    public DiseaseAdjDTO deleted;

    public DiseaseAdjDeleted() {
    }

    public DiseaseAdjDeleted(DiseaseAdjDTO deleted) {
        this.deleted = deleted;
    }
}