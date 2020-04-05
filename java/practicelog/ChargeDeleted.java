package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ChargeDTO;

public class ChargeDeleted implements PracticeLogBody {

    public ChargeDTO deleted;

    public ChargeDeleted() {
    }

    public ChargeDeleted(ChargeDTO deleted) {
        this.deleted = deleted;
    }
}