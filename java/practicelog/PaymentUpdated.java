package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.PaymentDTO;

public class PaymentUpdated implements PracticeLogBody {

    public PaymentDTO prev;
    public PaymentDTO updated;

    public PaymentUpdated() {
    }

    public PaymentUpdated(PaymentDTO prev, PaymentDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}