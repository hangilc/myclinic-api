package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.PaymentDTO;

public class PaymentCreated implements PracticeLogBody {

    public PaymentDTO created;

    public PaymentCreated() {
    }

    public PaymentCreated(PaymentDTO created) {
        this.created = created;
    }
}