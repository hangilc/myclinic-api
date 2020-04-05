package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.PharmaDrugDTO;

public class PharmaDrugDeleted implements PracticeLogBody {

    public PharmaDrugDTO deleted;

    public PharmaDrugDeleted() {
    }

    public PharmaDrugDeleted(PharmaDrugDTO deleted) {
        this.deleted = deleted;
    }
}