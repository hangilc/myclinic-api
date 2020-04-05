package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.PharmaQueueDTO;

public class PharmaQueueDeleted implements PracticeLogBody {

    public PharmaQueueDTO deleted;

    public PharmaQueueDeleted() {
    }

    public PharmaQueueDeleted(PharmaQueueDTO deleted) {
        this.deleted = deleted;
    }
}
