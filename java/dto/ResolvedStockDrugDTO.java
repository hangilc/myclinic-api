package dev.myclinic.dto;

public class ResolvedStockDrugDTO {

    public int queryIyakuhincode;
    public int resolvedIyakuhincode;

    public static ResolvedStockDrugDTO create(int query, int resolved){
        ResolvedStockDrugDTO result = new ResolvedStockDrugDTO();
        result.queryIyakuhincode = query;
        result.resolvedIyakuhincode = resolved;
        return result;
    }

    @Override
    public String toString() {
        return "ResolvedStockDrugDTO{" +
                "queryIyakuhincode=" + queryIyakuhincode +
                ", resolvedIyakuhincode=" + resolvedIyakuhincode +
                '}';
    }
}
