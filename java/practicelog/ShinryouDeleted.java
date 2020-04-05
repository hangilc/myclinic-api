package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ShinryouDTO;

public class ShinryouDeleted implements PracticeLogBody {

    public ShinryouDTO deleted;

    public ShinryouDeleted() {
    }

    public ShinryouDeleted(ShinryouDTO deleted) {
        this.deleted = deleted;
    }
}