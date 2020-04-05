package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ConductKizaiDTO;

public class ConductKizaiDeleted implements PracticeLogBody {

    public ConductKizaiDTO deleted;

    public ConductKizaiDeleted() {
    }

    public ConductKizaiDeleted(ConductKizaiDTO deleted) {
        this.deleted = deleted;
    }
}