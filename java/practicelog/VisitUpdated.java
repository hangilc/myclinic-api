package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.VisitDTO;

public class VisitUpdated implements PracticeLogBody {

    public VisitDTO prev;
    public VisitDTO updated;

    public VisitUpdated() {
    }

    public VisitUpdated(VisitDTO prev, VisitDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}