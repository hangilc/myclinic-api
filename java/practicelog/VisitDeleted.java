package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.VisitDTO;

public class VisitDeleted implements PracticeLogBody {

    public VisitDTO deleted;

    public VisitDeleted() {
    }

    public VisitDeleted(VisitDTO deleted) {
        this.deleted = deleted;
    }
}