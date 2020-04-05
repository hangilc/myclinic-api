package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ConductDrugDTO;

public class ConductDrugCreated implements PracticeLogBody {

    public ConductDrugDTO created;

    public ConductDrugCreated() {
    }

    public ConductDrugCreated(ConductDrugDTO created) {
        this.created = created;
    }
}