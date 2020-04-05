package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.VisitDTO;

public class VisitCreated implements PracticeLogBody {

    public VisitDTO created;

    public VisitCreated() {
    }

    public VisitCreated(VisitDTO created) {
        this.created = created;
    }
}