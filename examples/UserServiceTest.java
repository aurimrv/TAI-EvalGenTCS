package com.example.service;

import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Test class for UserService.
 */
public class UserServiceTest {
    
    private UserService userService = new UserService();
    
    @Test
    public void testCreateUser() {
        User user = userService.createUser("John Doe", "john@example.com");
        assertNotNull(user);
    }
    
    @Test
    public void testUpdateUser() {
        User user = userService.createUser("Jane", "jane@example.com");
        user.setName("Jane Doe");
        userService.updateUser(user);
        assertEquals("Jane Doe", user.getName());
    }
    
    @Test
    public void testDeleteUser() {
        User user = userService.createUser("Bob", "bob@example.com");
        userService.deleteUser(user.getId());
        assertNull(userService.findUser(user.getId()));
    }
}
