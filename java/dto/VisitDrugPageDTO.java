package dev.myclinic.dto;

import java.util.List;

public class VisitDrugPageDTO {

    public int page;
    public int totalPages;
    public List<VisitDrugDTO> visitDrugs;

    @Override
    public String toString() {
        return "VisitDrugPageDTO{" +
                "page=" + page +
                ", totalPages=" + totalPages +
                ", visitDrugs=" + visitDrugs +
                '}';
    }
}
