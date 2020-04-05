package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ConductKizaiDTO;

public class ConductKizaiCreated implements PracticeLogBody {

    public ConductKizaiDTO created;

    public ConductKizaiCreated(ConductKizaiDTO created) {
        this.created = created;
    }

    public ConductKizaiCreated() {
    }
}