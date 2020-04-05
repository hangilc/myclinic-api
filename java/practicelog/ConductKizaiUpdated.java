package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ConductKizaiDTO;

public class ConductKizaiUpdated implements PracticeLogBody {

    public ConductKizaiDTO prev;
    public ConductKizaiDTO updated;

    public ConductKizaiUpdated() {
    }

    public ConductKizaiUpdated(ConductKizaiDTO prev, ConductKizaiDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}