package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ChargeDTO;

public class ChargeCreated implements PracticeLogBody {

    public ChargeDTO created;

    public ChargeCreated() {
    }

    public ChargeCreated(ChargeDTO created) {
        this.created = created;
    }
}