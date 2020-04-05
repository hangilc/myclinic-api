package dev.myclinic.dto;

import dev.myclinic.dto.annotation.Primary;

public class IntraclinicTagPostDTO {
    @Primary
    public int tagId;
    @Primary
    public int postId;
}
