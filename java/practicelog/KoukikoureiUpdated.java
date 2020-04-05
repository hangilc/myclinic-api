package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.KoukikoureiDTO;

public class KoukikoureiUpdated implements PracticeLogBody {

    public KoukikoureiDTO prev;
    public KoukikoureiDTO updated;

    public KoukikoureiUpdated() {
    }

    public KoukikoureiUpdated(KoukikoureiDTO prev, KoukikoureiDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}