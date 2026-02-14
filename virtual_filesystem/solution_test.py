import unittest
from solution import VirtualFileSystem


class TestVirtualFileSystem(unittest.TestCase):

    def setUp(self):
        self.fs = VirtualFileSystem()

    # ==================== BASIC FILE OPERATIONS ====================

    def test_create_file_in_root(self):
        self.assertTrue(self.fs.create_file("/file.txt", "hello"))

    def test_read_file(self):
        self.fs.create_file("/file.txt", "hello world")
        self.assertEqual(self.fs.read_file("/file.txt"), "hello world")

    def test_read_nonexistent_file(self):
        self.assertIsNone(self.fs.read_file("/nonexistent.txt"))

    def test_delete_file(self):
        self.fs.create_file("/file.txt", "content")
        self.assertTrue(self.fs.delete("/file.txt"))
        self.assertIsNone(self.fs.read_file("/file.txt"))

    def test_delete_nonexistent(self):
        self.assertFalse(self.fs.delete("/nonexistent.txt"))

    def test_update_file_content(self):
        self.fs.create_file("/file.txt", "old")
        self.assertTrue(self.fs.write_file("/file.txt", "new"))
        self.assertEqual(self.fs.read_file("/file.txt"), "new")

    def test_write_to_nonexistent_file(self):
        self.assertFalse(self.fs.write_file("/nonexistent.txt", "data"))

    # ==================== DIRECTORY OPERATIONS ====================

    def test_create_directory(self):
        self.assertTrue(self.fs.mkdir("/documents"))

    def test_create_nested_directory(self):
        self.fs.mkdir("/documents")
        self.assertTrue(self.fs.mkdir("/documents/work"))

    def test_create_directory_without_parent(self):
        self.assertFalse(self.fs.mkdir("/documents/work/projects"))

    def test_mkdir_p_creates_parents(self):
        self.assertTrue(self.fs.mkdir_p("/a/b/c/d"))
        self.assertTrue(self.fs.create_file("/a/b/c/d/file.txt", "deep"))

    def test_list_directory(self):
        self.fs.mkdir("/docs")
        self.fs.create_file("/docs/a.txt", "")
        self.fs.create_file("/docs/b.txt", "")
        self.fs.mkdir("/docs/sub")
        result = self.fs.ls("/docs")
        self.assertEqual(sorted(result), ["a.txt", "b.txt", "sub"])

    def test_list_root(self):
        self.fs.create_file("/file1.txt", "")
        self.fs.mkdir("/folder")
        result = self.fs.ls("/")
        self.assertEqual(sorted(result), ["file1.txt", "folder"])

    def test_list_nonexistent_directory(self):
        self.assertIsNone(self.fs.ls("/nonexistent"))

    def test_list_file_returns_none(self):
        self.fs.create_file("/file.txt", "")
        self.assertIsNone(self.fs.ls("/file.txt"))

    def test_delete_empty_directory(self):
        self.fs.mkdir("/empty")
        self.assertTrue(self.fs.delete("/empty"))

    def test_delete_nonempty_directory_fails(self):
        self.fs.mkdir("/nonempty")
        self.fs.create_file("/nonempty/file.txt", "")
        self.assertFalse(self.fs.delete("/nonempty"))

    def test_delete_recursive(self):
        self.fs.mkdir_p("/a/b/c")
        self.fs.create_file("/a/b/c/file.txt", "")
        self.fs.create_file("/a/b/file2.txt", "")
        self.assertTrue(self.fs.delete_recursive("/a"))
        self.assertIsNone(self.fs.ls("/a"))

    # ==================== PATH RESOLUTION ====================

    def test_file_in_nested_directory(self):
        self.fs.mkdir_p("/home/user/documents")
        self.fs.create_file("/home/user/documents/notes.txt", "my notes")
        self.assertEqual(self.fs.read_file("/home/user/documents/notes.txt"), "my notes")

    def test_exists_file(self):
        self.fs.create_file("/file.txt", "")
        self.assertTrue(self.fs.exists("/file.txt"))

    def test_exists_directory(self):
        self.fs.mkdir("/folder")
        self.assertTrue(self.fs.exists("/folder"))

    def test_exists_nonexistent(self):
        self.assertFalse(self.fs.exists("/nonexistent"))

    def test_is_file(self):
        self.fs.create_file("/file.txt", "")
        self.assertTrue(self.fs.is_file("/file.txt"))

    def test_is_file_on_directory(self):
        self.fs.mkdir("/folder")
        self.assertFalse(self.fs.is_file("/folder"))

    def test_is_directory(self):
        self.fs.mkdir("/folder")
        self.assertTrue(self.fs.is_directory("/folder"))

    def test_is_directory_on_file(self):
        self.fs.create_file("/file.txt", "")
        self.assertFalse(self.fs.is_directory("/file.txt"))

    # ==================== MOVE AND COPY ====================

    def test_move_file(self):
        self.fs.mkdir("/dest")
        self.fs.create_file("/file.txt", "content")
        self.assertTrue(self.fs.move("/file.txt", "/dest/file.txt"))
        self.assertIsNone(self.fs.read_file("/file.txt"))
        self.assertEqual(self.fs.read_file("/dest/file.txt"), "content")

    def test_move_file_rename(self):
        self.fs.create_file("/old.txt", "data")
        self.assertTrue(self.fs.move("/old.txt", "/new.txt"))
        self.assertEqual(self.fs.read_file("/new.txt"), "data")
        self.assertFalse(self.fs.exists("/old.txt"))

    def test_move_directory(self):
        self.fs.mkdir_p("/src/sub")
        self.fs.create_file("/src/sub/file.txt", "nested")
        self.fs.mkdir("/dest")
        self.assertTrue(self.fs.move("/src", "/dest/src"))
        self.assertEqual(self.fs.read_file("/dest/src/sub/file.txt"), "nested")
        self.assertFalse(self.fs.exists("/src"))

    def test_move_into_self_fails(self):
        self.fs.mkdir_p("/a/b")
        self.assertFalse(self.fs.move("/a", "/a/b/a"))

    def test_move_nonexistent_fails(self):
        self.assertFalse(self.fs.move("/nonexistent", "/dest"))

    def test_copy_file(self):
        self.fs.create_file("/original.txt", "content")
        self.assertTrue(self.fs.copy("/original.txt", "/copy.txt"))
        self.assertEqual(self.fs.read_file("/original.txt"), "content")
        self.assertEqual(self.fs.read_file("/copy.txt"), "content")

    def test_copy_directory_recursive(self):
        self.fs.mkdir_p("/src/a/b")
        self.fs.create_file("/src/a/file.txt", "data")
        self.assertTrue(self.fs.copy("/src", "/dest"))
        self.assertEqual(self.fs.read_file("/dest/a/file.txt"), "data")
        self.assertTrue(self.fs.exists("/src/a/file.txt"))

    def test_copy_modifying_copy_doesnt_affect_original(self):
        self.fs.create_file("/original.txt", "original")
        self.fs.copy("/original.txt", "/copy.txt")
        self.fs.write_file("/copy.txt", "modified")
        self.assertEqual(self.fs.read_file("/original.txt"), "original")

    # ==================== SEARCH ====================

    def test_find_by_name(self):
        self.fs.mkdir_p("/a/b/c")
        self.fs.create_file("/a/target.txt", "")
        self.fs.create_file("/a/b/target.txt", "")
        self.fs.create_file("/a/b/c/other.txt", "")
        result = self.fs.find("/a", "target.txt")
        self.assertEqual(sorted(result), ["/a/b/target.txt", "/a/target.txt"])

    def test_find_no_matches(self):
        self.fs.mkdir("/folder")
        self.fs.create_file("/folder/file.txt", "")
        result = self.fs.find("/folder", "nonexistent.txt")
        self.assertEqual(result, [])

    def test_find_from_root(self):
        self.fs.mkdir_p("/x/y")
        self.fs.create_file("/x/y/needle.txt", "")
        self.fs.create_file("/needle.txt", "")
        result = self.fs.find("/", "needle.txt")
        self.assertEqual(sorted(result), ["/needle.txt", "/x/y/needle.txt"])

    def test_grep_finds_content(self):
        self.fs.mkdir("/docs")
        self.fs.create_file("/docs/a.txt", "hello world")
        self.fs.create_file("/docs/b.txt", "goodbye world")
        self.fs.create_file("/docs/c.txt", "hello there")
        result = self.fs.grep("/docs", "hello")
        self.assertEqual(sorted(result), ["/docs/a.txt", "/docs/c.txt"])

    def test_grep_no_matches(self):
        self.fs.create_file("/file.txt", "content")
        result = self.fs.grep("/", "nonexistent")
        self.assertEqual(result, [])

    # ==================== FILE SIZE AND DISK USAGE ====================

    def test_get_file_size(self):
        self.fs.create_file("/file.txt", "hello")
        self.assertEqual(self.fs.get_size("/file.txt"), 5)

    def test_get_directory_size(self):
        self.fs.mkdir("/dir")
        self.fs.create_file("/dir/a.txt", "hello")
        self.fs.create_file("/dir/b.txt", "world!")
        self.assertEqual(self.fs.get_size("/dir"), 11)

    def test_get_nested_directory_size(self):
        self.fs.mkdir_p("/dir/sub")
        self.fs.create_file("/dir/a.txt", "abc")
        self.fs.create_file("/dir/sub/b.txt", "defgh")
        self.assertEqual(self.fs.get_size("/dir"), 8)

    def test_total_disk_usage(self):
        self.fs.create_file("/a.txt", "12345")
        self.fs.mkdir("/dir")
        self.fs.create_file("/dir/b.txt", "67890")
        self.assertEqual(self.fs.disk_usage(), 10)

    # ==================== QUOTA SYSTEM ====================

    def test_set_quota(self):
        self.assertTrue(self.fs.set_quota(100))

    def test_create_file_within_quota(self):
        self.fs.set_quota(100)
        self.assertTrue(self.fs.create_file("/file.txt", "x" * 50))

    def test_create_file_exceeds_quota(self):
        self.fs.set_quota(10)
        self.assertFalse(self.fs.create_file("/file.txt", "x" * 20))
        self.assertFalse(self.fs.exists("/file.txt"))

    def test_write_exceeds_quota(self):
        self.fs.set_quota(20)
        self.fs.create_file("/file.txt", "small")
        self.assertFalse(self.fs.write_file("/file.txt", "x" * 30))
        self.assertEqual(self.fs.read_file("/file.txt"), "small")

    def test_copy_exceeds_quota(self):
        self.fs.set_quota(15)
        self.fs.create_file("/file.txt", "x" * 10)
        self.assertFalse(self.fs.copy("/file.txt", "/copy.txt"))

    def test_quota_freed_on_delete(self):
        self.fs.set_quota(20)
        self.fs.create_file("/file.txt", "x" * 15)
        self.fs.delete("/file.txt")
        self.assertTrue(self.fs.create_file("/new.txt", "x" * 15))

    # ==================== PERMISSIONS ====================

    def test_set_permissions(self):
        self.fs.create_file("/file.txt", "content")
        self.assertTrue(self.fs.chmod("/file.txt", "r"))

    def test_read_only_file_cannot_be_written(self):
        self.fs.create_file("/file.txt", "original")
        self.fs.chmod("/file.txt", "r")
        self.assertFalse(self.fs.write_file("/file.txt", "new"))
        self.assertEqual(self.fs.read_file("/file.txt"), "original")

    def test_read_only_file_can_be_read(self):
        self.fs.create_file("/file.txt", "content")
        self.fs.chmod("/file.txt", "r")
        self.assertEqual(self.fs.read_file("/file.txt"), "content")

    def test_no_permission_file_cannot_be_read(self):
        self.fs.create_file("/secret.txt", "secret")
        self.fs.chmod("/secret.txt", "")
        self.assertIsNone(self.fs.read_file("/secret.txt"))

    def test_write_only_file(self):
        self.fs.create_file("/file.txt", "original")
        self.fs.chmod("/file.txt", "w")
        self.assertIsNone(self.fs.read_file("/file.txt"))
        self.assertTrue(self.fs.write_file("/file.txt", "new"))

    def test_read_only_file_cannot_be_deleted(self):
        self.fs.create_file("/file.txt", "content")
        self.fs.chmod("/file.txt", "r")
        self.assertFalse(self.fs.delete("/file.txt"))

    def test_restore_permissions(self):
        self.fs.create_file("/file.txt", "content")
        self.fs.chmod("/file.txt", "r")
        self.fs.chmod("/file.txt", "rw")
        self.assertTrue(self.fs.write_file("/file.txt", "new"))

    # ==================== SYMBOLIC LINKS ====================

    def test_create_symlink(self):
        self.fs.create_file("/target.txt", "content")
        self.assertTrue(self.fs.symlink("/target.txt", "/link.txt"))

    def test_read_through_symlink(self):
        self.fs.create_file("/target.txt", "content")
        self.fs.symlink("/target.txt", "/link.txt")
        self.assertEqual(self.fs.read_file("/link.txt"), "content")

    def test_write_through_symlink(self):
        self.fs.create_file("/target.txt", "old")
        self.fs.symlink("/target.txt", "/link.txt")
        self.fs.write_file("/link.txt", "new")
        self.assertEqual(self.fs.read_file("/target.txt"), "new")

    def test_symlink_to_directory(self):
        self.fs.mkdir("/realdir")
        self.fs.create_file("/realdir/file.txt", "data")
        self.fs.symlink("/realdir", "/linkdir")
        self.assertEqual(self.fs.read_file("/linkdir/file.txt"), "data")

    def test_broken_symlink(self):
        self.fs.create_file("/target.txt", "content")
        self.fs.symlink("/target.txt", "/link.txt")
        self.fs.delete("/target.txt")
        self.assertIsNone(self.fs.read_file("/link.txt"))

    def test_symlink_chain(self):
        self.fs.create_file("/file.txt", "data")
        self.fs.symlink("/file.txt", "/link1.txt")
        self.fs.symlink("/link1.txt", "/link2.txt")
        self.assertEqual(self.fs.read_file("/link2.txt"), "data")

    def test_circular_symlink_detection(self):
        self.fs.mkdir("/dir")
        self.fs.symlink("/dir", "/dir/link")
        self.assertIsNone(self.fs.read_file("/dir/link/link/link/file.txt"))

    def test_is_symlink(self):
        self.fs.create_file("/target.txt", "")
        self.fs.symlink("/target.txt", "/link.txt")
        self.assertTrue(self.fs.is_symlink("/link.txt"))
        self.assertFalse(self.fs.is_symlink("/target.txt"))

    def test_readlink(self):
        self.fs.create_file("/target.txt", "")
        self.fs.symlink("/target.txt", "/link.txt")
        self.assertEqual(self.fs.readlink("/link.txt"), "/target.txt")

    def test_readlink_on_regular_file(self):
        self.fs.create_file("/file.txt", "")
        self.assertIsNone(self.fs.readlink("/file.txt"))

    # ==================== ADVANCED OPERATIONS ====================

    def test_tree_structure(self):
        self.fs.mkdir_p("/a/b/c")
        self.fs.create_file("/a/file1.txt", "")
        self.fs.create_file("/a/b/file2.txt", "")
        tree = self.fs.tree("/a")
        expected = {
            "name": "a",
            "type": "directory",
            "children": [
                {
                    "name": "b",
                    "type": "directory",
                    "children": [
                        {
                            "name": "c",
                            "type": "directory",
                            "children": []
                        },
                        {
                            "name": "file2.txt",
                            "type": "file"
                        }
                    ]
                },
                {
                    "name": "file1.txt",
                    "type": "file"
                }
            ]
        }
        self.assertEqual(tree, expected)

    def test_diff_files(self):
        self.fs.create_file("/a.txt", "line1\nline2\nline3")
        self.fs.create_file("/b.txt", "line1\nmodified\nline3")
        diff = self.fs.diff("/a.txt", "/b.txt")
        self.assertIn("line2", diff)
        self.assertIn("modified", diff)

    def test_append_to_file(self):
        self.fs.create_file("/file.txt", "hello")
        self.assertTrue(self.fs.append("/file.txt", " world"))
        self.assertEqual(self.fs.read_file("/file.txt"), "hello world")

    def test_append_to_nonexistent(self):
        self.assertFalse(self.fs.append("/nonexistent.txt", "data"))

    def test_truncate_file(self):
        self.fs.create_file("/file.txt", "hello world")
        self.assertTrue(self.fs.truncate("/file.txt", 5))
        self.assertEqual(self.fs.read_file("/file.txt"), "hello")

    def test_truncate_longer_than_file(self):
        self.fs.create_file("/file.txt", "hi")
        self.assertTrue(self.fs.truncate("/file.txt", 10))
        self.assertEqual(self.fs.read_file("/file.txt"), "hi")

    def test_get_parent(self):
        self.fs.mkdir_p("/a/b/c")
        self.assertEqual(self.fs.get_parent("/a/b/c"), "/a/b")

    def test_get_parent_of_root(self):
        self.assertIsNone(self.fs.get_parent("/"))

    def test_get_absolute_path(self):
        self.fs.mkdir_p("/home/user")
        self.fs.cd("/home/user")
        self.fs.create_file("/home/user/file.txt", "")
        self.assertEqual(self.fs.get_absolute_path("file.txt"), "/home/user/file.txt")

    def test_cd_and_relative_operations(self):
        self.fs.mkdir_p("/home/user/documents")
        self.fs.cd("/home/user")
        self.assertTrue(self.fs.create_file("file.txt", "content"))
        self.assertEqual(self.fs.read_file("file.txt"), "content")
        self.assertEqual(self.fs.read_file("/home/user/file.txt"), "content")

    def test_cd_with_parent_reference(self):
        self.fs.mkdir_p("/home/user/documents")
        self.fs.cd("/home/user/documents")
        self.fs.cd("..")
        self.fs.create_file("test.txt", "data")
        self.assertEqual(self.fs.read_file("/home/user/test.txt"), "data")

    def test_pwd(self):
        self.fs.mkdir_p("/home/user")
        self.fs.cd("/home/user")
        self.assertEqual(self.fs.pwd(), "/home/user")

    def test_pwd_initial(self):
        self.assertEqual(self.fs.pwd(), "/")
    


if __name__ == '__main__':
    unittest.main()
