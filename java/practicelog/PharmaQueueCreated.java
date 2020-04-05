package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.PharmaQueueDTO;

public class PharmaQueueCreated implements PracticeLogBody {

    public PharmaQueueDTO created;

    public PharmaQueueCreated() {
    }

    public PharmaQueueCreated(PharmaQueueDTO created) {
        this.created = created;
    }
}
