package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ShahokokuhoDTO;

public class ShahokokuhoDeleted implements PracticeLogBody {

    public ShahokokuhoDTO deleted;

    public ShahokokuhoDeleted() {
    }

    public ShahokokuhoDeleted(ShahokokuhoDTO deleted) {
        this.deleted = deleted;
    }
}
