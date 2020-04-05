package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.DiseaseDTO;

public class DiseaseDeleted implements PracticeLogBody {

    public DiseaseDTO deleted;

    public DiseaseDeleted() {
    }

    public DiseaseDeleted(DiseaseDTO deleted) {
        this.deleted = deleted;
    }
}