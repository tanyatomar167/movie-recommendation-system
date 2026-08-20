function Sidebar({ activePage, setActivePage, stats }) {
  const menuItems = [
    { id: "dashboard", label: "Dashboard", icon: "⌂" },
    { id: "recommend", label: "Recommendations", icon: "★" },
    { id: "similar", label: "Similar Movies", icon: "◈" },
    { id: "browse", label: "Browse Movies", icon: "▦" },
  ];

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">🎬</div>
        <div>
          <h2>MovieRec</h2>
          <span>AI Recommendation</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${
              activePage === item.id ? "active" : ""
            }`}
            onClick={() => setActivePage(item.id)}
          >
            <span>{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>

      <div className="sidebar-stats">
        <p className="sidebar-title">DATASET</p>

        <div className="sidebar-stat">
          <span>Users</span>
          <strong>{stats?.users ?? "—"}</strong>
        </div>

        <div className="sidebar-stat">
          <span>Movies</span>
          <strong>{stats?.movies ?? "—"}</strong>
        </div>

        <div className="sidebar-stat">
          <span>Ratings</span>
          <strong>{stats?.ratings ?? "—"}</strong>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;