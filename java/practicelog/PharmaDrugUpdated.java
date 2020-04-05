package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.PharmaDrugDTO;

public class PharmaDrugUpdated implements PracticeLogBody {

    public PharmaDrugDTO prev;
    public PharmaDrugDTO updated;

    public PharmaDrugUpdated() {
    }

    public PharmaDrugUpdated(PharmaDrugDTO prev, PharmaDrugDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}