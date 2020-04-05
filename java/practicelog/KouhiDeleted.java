package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.KouhiDTO;

public class KouhiDeleted implements PracticeLogBody {

    public KouhiDTO deleted;

    public KouhiDeleted() {
    }

    public KouhiDeleted(KouhiDTO deleted) {
        this.deleted = deleted;
    }
}