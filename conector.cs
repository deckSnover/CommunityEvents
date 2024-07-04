// Models/Message.cs
public class Message
{
    public int Id { get; set; }
    public string Sender { get; set; }
    public string Receiver { get; set; }
    public string Content { get; set; }
    public DateTime Timestamp { get; set; }
}

// Repositories/IMessageRepository.cs
public interface IMessageRepository
{
    Task<IEnumerable<Message>> GetMessages(string sender, string receiver);
    Task<Message> SendMessage(Message message);
}

// Repositories/MessageRepository.cs
public class MessageRepository : IMessageRepository
{
    private readonly CommunityEventsContext _context;

    public MessageRepository(CommunityEventsContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<Message>> GetMessages(string sender, string receiver)
    {
        return await _context.Messages
            .Where(m => (m.Sender == sender && m.Receiver == receiver) || (m.Sender == receiver && m.Receiver == sender))
            .OrderBy(m => m.Timestamp)
            .ToListAsync();
    }

    public async Task<Message> SendMessage(Message message)
    {
        _context.Messages.Add(message);
        await _context.SaveChangesAsync();
        return message;
    }
}

// Controllers/ChatController.cs
[ApiController]
[Route("api/[controller]")]
public class ChatController : ControllerBase
{
    private readonly IMessageRepository _messageRepository;

    public ChatController(IMessageRepository messageRepository)
    {
        _messageRepository = messageRepository;
    }

    [HttpGet("{sender}/{receiver}")]
    public async Task<ActionResult<IEnumerable<Message>>> GetMessages(string sender, string receiver)
    {
        return await _messageRepository.GetMessages(sender, receiver);
    }

    [HttpPost]
    public async Task<ActionResult<Message>> SendMessage(Message message)
    {
        return await _messageRepository.SendMessage(message);
    }
}

// Updating CommunityEventsContext to include Messages
public class CommunityEventsContext : DbContext
{
    public CommunityEventsContext(DbContextOptions<CommunityEventsContext> options) : base(options)
    {
    }

    public DbSet<Event> Events { get; set; }
    public DbSet<Message> Messages { get; set; }
}