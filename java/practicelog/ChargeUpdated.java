package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ChargeDTO;

public class ChargeUpdated implements PracticeLogBody {

    public ChargeDTO prev;
    public ChargeDTO updated;

    public ChargeUpdated() {
    }

    public ChargeUpdated(ChargeDTO prev, ChargeDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}