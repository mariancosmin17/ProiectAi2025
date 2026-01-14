import React, { useMemo, useState } from "react";

/**
 * Nod: { type?: "MAX"|"MIN", children?: Node[], value?: number }
 * - frunză: children null/undefined și value setat
 * - nod intern: type setat și children array
 */

function isLeaf(node) {
  return !node?.children || node.children.length === 0;
}

function label(node) {
  return isLeaf(node) ? `🍃 ${node.value}` : node.type;
}

function NodeBox({ node, depth, path, collapsed, toggle }) {
  const leaf = isLeaf(node);

  return (
    <div style={{ display: "flex", alignItems: "flex-start", gap: 10 }}>
      {/* linie verticală + conector */}
      <div style={{ width: 18, display: "flex", flexDirection: "column", alignItems: "center" }}>
        {depth > 0 && (
          <>
            <div style={{ width: 2, flex: 1, background: "#d1d5db" }} />
            <div style={{ width: 10, height: 2, background: "#d1d5db" }} />
          </>
        )}
      </div>

      <div style={{ flex: 1 }}>
        {/* box nod */}
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 8,
            padding: "8px 12px",
            borderRadius: 10,
            border: "1px solid #e5e7eb",
            background: leaf ? "#f9fafb" : "#ffffff",
            boxShadow: "0 2px 10px rgba(0,0,0,0.04)",
            fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Arial",
            fontSize: 14,
            fontWeight: leaf ? 600 : 700,
          }}
        >
          {!leaf && (
            <button
              onClick={() => toggle(path)}
              style={{
                border: "none",
                background: "#111827",
                color: "white",
                width: 22,
                height: 22,
                borderRadius: 6,
                cursor: "pointer",
                fontSize: 12,
                lineHeight: "22px",
              }}
              title={collapsed ? "Extinde" : "Restrânge"}
            >
              {collapsed ? "+" : "−"}
            </button>
          )}
          <span>{label(node)}</span>
        </div>

        {/* copii */}
        {!leaf && !collapsed && (
          <div style={{ marginTop: 10, marginLeft: 16, display: "flex", flexDirection: "column", gap: 10 }}>
            {node.children.map((child, idx) => (
              <TreeNode
                key={idx}
                node={child}
                depth={depth + 1}
                path={`${path}.${idx}`}
                toggle={toggle}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function TreeNode({ node, depth = 0, path = "0", toggle }) {
  const [collapsedMap, setCollapsedMap] = useState({});

  const collapsed = !!collapsedMap[path];

  // toggle local per nod
  const localToggle = (p) => {
    setCollapsedMap((prev) => ({ ...prev, [p]: !prev[p] }));
  };

  return (
    <NodeBox
      node={node}
      depth={depth}
      path={path}
      collapsed={collapsed}
      toggle={localToggle}
    />
  );
}

export default function TreeView({ tree }) {
  const treeOk = useMemo(() => tree && typeof tree === "object", [tree]);

  if (!treeOk) {
    return (
      <div style={{ padding: 12, border: "1px dashed #cbd5e1", borderRadius: 10 }}>
        Arbore indisponibil.
      </div>
    );
  }

  return (
    <div
      style={{
        padding: 14,
        borderRadius: 12,
        border: "1px solid #e5e7eb",
        background: "white",
      }}
    >
      <TreeNode node={tree} />
      <div style={{ marginTop: 10, fontSize: 12, opacity: 0.75 }}>
        (Nod intern: type=MAX/MIN, frunză: value)
      </div>
    </div>
  );
}
