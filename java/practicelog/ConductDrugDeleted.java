package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ConductDrugDTO;

public class ConductDrugDeleted implements PracticeLogBody {

    public ConductDrugDTO deleted;

    public ConductDrugDeleted() {
    }

    public ConductDrugDeleted(ConductDrugDTO deleted) {
        this.deleted = deleted;
    }
}