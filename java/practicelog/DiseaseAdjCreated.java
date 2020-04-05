package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.DiseaseAdjDTO;

public class DiseaseAdjCreated implements PracticeLogBody {

    public DiseaseAdjDTO created;

    public DiseaseAdjCreated() {
    }

    public DiseaseAdjCreated(DiseaseAdjDTO created) {
        this.created = created;
    }
}