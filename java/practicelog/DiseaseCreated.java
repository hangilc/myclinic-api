package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.DiseaseDTO;

public class DiseaseCreated implements PracticeLogBody {

    public DiseaseDTO created;

    public DiseaseCreated() {
    }

    public DiseaseCreated(DiseaseDTO created) {
        this.created = created;
    }
}