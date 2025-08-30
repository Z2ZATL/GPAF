# Updating GPAF

This guide explains how to update GPAF to the latest version.

## Update Methods

### Docker Update

1. **Pull Latest Image**
   ```bash
   docker pull frdel/gpaf-run
   ```

2. **Stop Current Container**
   - Stop the running container
   - Remove the old container

3. **Start New Container**
   - Use the same volume mapping
   - Keep your data directory

### Manual Update

1. **Backup Data**
   - Copy your data directory
   - Save settings
   - Export important files

2. **Update Files**
   - Pull latest changes
   - Update dependencies
   - Verify configurations

3. **Restore Data**
   - Copy back your data
   - Update settings
   - Test functionality

## Data Preservation

### What's Preserved

- Memory data
- Knowledge base
- Settings
- Custom prompts
- Work files

### What's Updated

- Core framework
- Dependencies
- Documentation
- Tools
- Extensions

## Troubleshooting

### Common Issues

1. **Update Failures**
   - Check permissions
   - Verify space
   - Test connectivity
   - Review logs

2. **Data Issues**
   - Verify backups
   - Check integrity
   - Test functionality
   - Restore if needed

## Resources

- [Documentation](https://github.com/frdel/gpaf/docs)
- [Discord Community](https://discord.gg/Z2tun2N3)
- [Skool](https://www.skool.com/gpaf)
- [Issue Tracker](https://github.com/frdel/gpaf/issues)

For update issues, contact the maintainers. 