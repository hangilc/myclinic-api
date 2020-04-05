package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.PaymentDTO;

public class PaymentDeleted implements PracticeLogBody {

    public PaymentDTO deleted;

    public PaymentDeleted() {
    }

    public PaymentDeleted(PaymentDTO deleted) {
        this.deleted = deleted;
    }
}