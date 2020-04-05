package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.PharmaDrugDTO;

public class PharmaDrugCreated implements PracticeLogBody {

    public PharmaDrugDTO created;

    public PharmaDrugCreated() {
    }

    public PharmaDrugCreated(PharmaDrugDTO created) {
        this.created = created;
    }
}