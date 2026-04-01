package com.example;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

public class ExampleTest {

  @Test
  public void additionIsCorrect() {
    assertEquals(4, 2 + 2);
  }

  @Test
  public void stringConcatenation() {
    assertEquals("hello world", "hello" + " " + "world");
  }

  @Test
  public void listIsNotEmpty() {
    var items = java.util.List.of("a", "b", "c");
    assertTrue(items.size() == 3);
  }
}
