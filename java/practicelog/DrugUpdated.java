package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.DrugDTO;

public class DrugUpdated implements PracticeLogBody {

    public DrugDTO prev;
    public DrugDTO updated;

    public DrugUpdated() {
    }

    public DrugUpdated(DrugDTO prev, DrugDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}