package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ConductDrugDTO;

public class ConductDrugUpdated implements PracticeLogBody {

    public ConductDrugDTO prev;
    public ConductDrugDTO updated;

    public ConductDrugUpdated() {
    }

    public ConductDrugUpdated(ConductDrugDTO prev, ConductDrugDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}