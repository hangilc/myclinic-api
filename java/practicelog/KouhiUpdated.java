package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.KouhiDTO;

public class KouhiUpdated implements PracticeLogBody {

    public KouhiDTO prev;
    public KouhiDTO updated;

    public KouhiUpdated() {
    }

    public KouhiUpdated(KouhiDTO prev, KouhiDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}